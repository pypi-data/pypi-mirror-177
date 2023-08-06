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

r'''A layer that produces a dense `Tensor` based on given `feature_columns`.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.feature_column import feature_column as fc_old
from tensorflow.python.feature_column import feature_column_v2 as fc
from tensorflow.python.framework import ops
from tensorflow.python.ops import array_ops

from hybridbackend.tensorflow.feature_column.backend import EmbeddingBackend
from hybridbackend.tensorflow.feature_column.feature_column import \
  EmbeddingColumn
from hybridbackend.tensorflow.feature_column.feature_column import \
  SharedEmbeddingColumn
from hybridbackend.tensorflow.feature_column.feature_column import \
  StateManagerImpl

# pylint: disable=ungrouped-imports
try:
  from tensorflow.python.feature_column.dense_features import \
    DenseFeatures as _DenseFeatures
except ImportError:
  from tensorflow.python.feature_column.feature_column_v2 import \
    FeatureLayer as _DenseFeatures
# pylint: enable=ungrouped-imports


class DenseFeatures(_DenseFeatures):
  r'''A layer that produces a dense `Tensor` based on given `feature_columns`.
  '''
  def __init__(self, feature_columns, trainable=True, name=None, **kwargs):
    r'''Constructs a DenseFeatures layer.
    '''
    self._impl = EmbeddingBackend.get()
    self._enable_concat = kwargs.pop('enable_concat', self._impl.enable_concat)
    verified_feature_columns = []
    for f in feature_columns:
      if isinstance(f, fc.EmbeddingColumn):
        verified_feature_columns.append(EmbeddingColumn.build(f))
      elif isinstance(f, fc_old._SharedEmbeddingColumn):
        verified_feature_columns.append(SharedEmbeddingColumn.build(f))
      elif isinstance(f, fc.SharedEmbeddingColumn):
        raise ValueError(
          f'{f} not supported: Use tf.feature_column.shared_embeding_columns')
      else:
        verified_feature_columns.append(f)
    super().__init__(
      feature_columns=verified_feature_columns,
      trainable=trainable,
      name=name,
      **kwargs)
    self._state_manager = StateManagerImpl(self, self.trainable)  # pylint: disable=protected-access

  def call(self, features, cols_to_output_tensors=None):
    r'''Returns a dense tensor corresponding to the `feature_columns`.

    Args:
      features: A mapping from key to tensors. `FeatureColumn`s look up via
        these keys. For example `numeric_column('price')` will look at 'price'
        key in this dict. Values can be a `SparseTensor` or a `Tensor` depends
        on corresponding `FeatureColumn`.
      cols_to_output_tensors: If not `None`, this will be filled with a dict
        mapping feature columns to output tensors created.

    Returns:
      A `Tensor` which represents input layer of a model. Its shape
      is (batch_size, first_layer_dimension) and its dtype is `float32`.
      first_layer_dimension is determined based on given `feature_columns`.
      If emb_enable_concat is disabled, `None` would be returned.

    Raises:
      ValueError: If arguments are not valid.
    '''
    if not isinstance(features, dict):
      raise ValueError('We expected a dictionary here. Instead we got: ',
                       features)

    for k, v in features.items():
      if (isinstance(v, ops.Tensor)
          and v.shape.rank is not None
          and v.shape.rank > 1):
        raise TypeError(
          f'Column {k} has a multi-rank tf.Tensor input, please uses '
          'tf.sparse.SparseTensor instead')

    transformation_cache = fc.FeatureTransformationCache(features)
    indexed_non_coalesced_columns = []
    for cid, c in enumerate(self._feature_columns):
      indexed_non_coalesced_columns.append(tuple([cid, c]))

    output_tensors = []
    with ops.name_scope(self.name):
      for c in self._feature_columns:
        with ops.name_scope(c.name):
          tensor = c.get_dense_tensor(transformation_cache, self._state_manager)
          if hasattr(self, '_process_dense_tensor'):
            processed_tensors = self._process_dense_tensor(c, tensor)
          else:
            processed_tensors = tensor
          if cols_to_output_tensors is not None:
            cols_to_output_tensors[c] = processed_tensors
          output_tensors.append(processed_tensors)

    if not self._enable_concat:
      return output_tensors

    if hasattr(self, '_verify_and_concat_tensors'):
      return self._verify_and_concat_tensors(output_tensors)
    return array_ops.concat(output_tensors, 1)


def dense_features(features, feature_columns):
  r'''Function produces dense tensors based on given `feature_columns`.

  Args:
    features: A mapping from key to tensors. `FeatureColumn`s look up via
      these keys. For example `numeric_column('price')` will look at 'price'
      key in this dict. Values can be a `SparseTensor` or a `Tensor` depends
      on corresponding `FeatureColumn`.
    feature_columns: List of feature columns.

  Returns:
    List of `Tensor`s which represents input layer of a model, which matches
    order of columns in `feature_columns`.
  '''
  cols_to_output_tensors = {}
  DenseFeatures(feature_columns)(
    features, cols_to_output_tensors=cols_to_output_tensors)
  return [cols_to_output_tensors[f] for f in feature_columns]
