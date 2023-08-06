// Copyright (c) 2022 CESNET
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import * as React from 'react'
import _isArray from 'lodash/isArray'

/**
 */
const withDataArray = (Component) => ({ data, useGlobalData, ...rest }) => {
  return _isArray(data) ? (
    data.map((d, idx) => (
      <Component key={idx} {...{ data: d, useGlobalData }} {...rest} />
    ))
  ) : (
    <Component {...{ data, useGlobalData }} {...rest} />
  )
}

export default withDataArray
