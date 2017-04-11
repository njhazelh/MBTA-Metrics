import React from 'react';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';
import store from '../store';
import { connect } from 'react-redux';
import * as filterActions from '../actions/filterActions';
import { LINES } from '../constants';

class LineSelector extends React.Component {
  selectAll() {
    LINES.forEach(line =>
      store.dispatch(filterActions.setLineFilter(line, true)));
  }

  resetAll() {
    LINES.forEach(line =>
      store.dispatch(filterActions.setLineFilter(line, false)));
  }

  setLineFilter(e) {
    const {value, checked} = e.target;
    store.dispatch(filterActions.setLineFilter(value, checked));
  }

  render() {
    const {filters} = this.props;
    return (
      <fieldset className="my-3">
        <legend>
          Lines:
          <Button outline color="primary" className="togglebutton" onClick={this.selectAll}>All</Button>
          <Button outline color="warning" className="togglebutton" onClick={this.resetAll}>None</Button>
        </legend>
        <Form>
          <Row>
            {
              LINES.map(line =>
                <Col xs={6} md={4} lg={3} key={line}>
                  <Label check style={{whiteSpace: 'nowrap'}}>
                    <Input
                      type='checkbox'
                      name={line}
                      value={line}
                      // !! for undefined -> false
                      // This makes sure that the component is always controlled.
                      checked={!!filters[line]}
                      onChange={this.setLineFilter}
                    />
                    {' '}
                    {line}
                  </Label>
                </Col>
              )
            }
          </Row>
        </Form>
      </fieldset>
    );
  }
}

export default connect(store => {
  return {filters: store.lineFilters};
})(LineSelector);
