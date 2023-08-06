# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

r'''Functors for embedding lookup.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import ops
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.ops import array_ops
from tensorflow.python.platform import tf_logging as logging

from hybridbackend.tensorflow.distribute.collective import Collective
from hybridbackend.tensorflow.feature_column.backend import EmbeddingBackend
from hybridbackend.tensorflow.feature_column.math_lib import segment_reduce
from hybridbackend.tensorflow.framework.context import Context
from hybridbackend.tensorflow.ops.floormod_shuffle.ops import floormod_shuffle


class EmbeddingLookup(object):  # pylint: disable=useless-object-inheritance
  r'''Functor to lookup embeddings.
  '''
  def __init__(self):
    self._impl = EmbeddingBackend.get()

  def __call__(self, column, weights, inputs, name=None):
    r'''Lookup embedding results for sparse tensors.
    '''
    with ops.name_scope(name):
      sparse_ids = inputs.id_tensor
      sparse_weights = inputs.weight_tensor
      if isinstance(sparse_ids, sparse_tensor.SparseTensor):
        ids = sparse_ids.values
      else:
        ids = sparse_ids
      input_device = self._impl.input_device(column)
      pad = self._impl.pad(column)
      segment_rank = self._impl.segment_rank(column)
      with ops.device(input_device):
        ids = array_ops.reshape(ops.convert_to_tensor(ids), [-1])
        if self._impl.unique(column):
          unique_index = None
          if not pad:
            logging.info('If unique is set to True, pad would be set to True')
            pad = True
        else:
          ids, unique_index = array_ops.unique(ids)
        if segment_rank != 0 and not pad:
          logging.info('If segment rank is not 0, pad would be set to True')
          pad = True
      dimension = self._impl.dimension(column)
      if self._impl.sharded(column):
        with ops.name_scope('shuffle_ids'):
          ids_shards, ids_sizes, partition_index = floormod_shuffle(
            ids, Context.get().world_size)
          shard_ids, embs_sizes = Collective.get().alltoall(
            ids_shards, sizes=ids_sizes)
          shard_ids, shard_unique_index = array_ops.unique(shard_ids)
        with ops.device(self._impl.device(column)):
          with Context.scope(sharding=False):
            shard_embs = self._impl.lookup(
              column, weights, shard_ids, sharded=True)
        with ops.name_scope('shuffle_embeddings'):
          if shard_unique_index is not None:
            shard_embs = array_ops.gather(
              shard_embs, shard_unique_index, name='restore_unique')
          embs_shards, _ = Collective.get().alltoall(
            shard_embs,
            sizes=embs_sizes,
            common_shape=[dimension])
          embeddings = array_ops.gather(
            embs_shards, partition_index, name='restore_shuffle')
      else:
        with ops.device(self._impl.device(column)):
          with Context.scope(sharding=False):
            embeddings = self._impl.lookup(column, weights, ids)
      return segment_reduce(
        sparse_ids, embeddings,
        weights=sparse_weights,
        indices=unique_index,
        dimension=dimension,
        pad=pad,
        segment_rank=segment_rank,
        combiner=self._impl.combiner(column))
