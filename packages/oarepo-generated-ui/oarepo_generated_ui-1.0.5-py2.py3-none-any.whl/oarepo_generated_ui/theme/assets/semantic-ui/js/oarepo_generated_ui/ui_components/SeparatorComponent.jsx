// Copyright (c) 2022 CESNET
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

import * as React from 'react'
import PropTypes from 'prop-types'
import { useSeparator } from '../hooks'

/**
 * An Icon, that renders either as a custom
 * SVG graphic or as a built-in Semantic-UI Icon.
 */
const SeparatorComponent = ({ component }) => useSeparator(component)

SeparatorComponent.propTypes = {
  component: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
}

export default SeparatorComponent
