import React from 'react';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';
import { connect } from 'react-redux';

import store from '../store';
import * as filterActions from '../actions/filterActions';
import { LINES, LINE_KEYS } from '../constants';

class LineSelector extends React.Component {
  static selectAll() {
    store.dispatch(filterActions.setAllLineFilters(true));
  }

  static resetAll() {
    store.dispatch(filterActions.setAllLineFilters(false));
  }

  static setLineFilter(e) {
    const { value, checked } = e.target;
    store.dispatch(filterActions.setLineFilter(value, checked));
  }

  constructor() {
    super();
    LineSelector.selectAll();
  }

  render() {
    const { filters } = this.props;
    return (
      <fieldset className="my-3">
        <legend>
          Lines:
          <Button
            outline
            color="primary"
            className="togglebutton"
            onClick={LineSelector.selectAll}
          >
            All
          </Button>
          <Button
            outline
            color="warning"
            className="togglebutton"
            onClick={LineSelector.resetAll}
          >
            None
          </Button>
        </legend>
        <Form>
          <Row>
            {
              LINE_KEYS.map(line =>
                <Col xs={12} sm={6} md={4} lg={3} key={line}>
                  <Label check style={{ whiteSpace: 'nowrap' }}>
                    <Input
                      type="checkbox"
                      value={LINES[line]}
                      // !! for undefined -> false
                      // This makes sure that the component is always controlled.
                      checked={!!filters[LINES[line]]}
                      onChange={LineSelector.setLineFilter}
                    />
                    {' '}
                    {line}
                  </Label>
                </Col>,
              )
            }
          </Row>
        </Form>
      </fieldset>
    );
  }
}

export default connect(data => ({ filters: data.lineFilters }))(LineSelector);
