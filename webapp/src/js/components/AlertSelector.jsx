import React from 'react';
import { Row, Col, Label, Input, Form, Button } from 'reactstrap';
import store from '../store';
import { connect } from 'react-redux';
import * as filterActions from '../actions/filterActions';
import { ALERTS } from '../constants';

class AlertSelector extends React.Component {
  selectAll() {
    ALERTS.forEach(alert =>
      store.dispatch(filterActions.setAlertFilter(alert, true)));
  }

  resetAll() {
    ALERTS.forEach(alert =>
      store.dispatch(filterActions.setAlertFilter(alert, false)));
  }

  setAlertFilter(e) {
    const {value, checked} = e.target;
    store.dispatch(filterActions.setAlertFilter(value, checked));
  }

  render() {
    const {filters} = this.props;
    return (
        <fieldset className="my-3">
          <legend>
            Alerts:
            <Button outline color="primary" className="togglebutton" onClick={this.selectAll}>All</Button>
            <Button outline color="warning" className="togglebutton" onClick={this.resetAll}>None</Button>
          </legend>
          <Form>
            <Row>
              {
                ALERTS.map(alert =>
                  <Col xs={6} key={alert}>
                    <Label check>
                      <Input
                        type='checkbox'
                        name={alert}
                        value={alert}
                        // !! for undefined -> false
                        // This makes sure that the component is always controlled.
                        checked={!!filters[alert]}
                        onChange={this.setAlertFilter}
                      />
                      {' '}
                      {alert}
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
  return {filters: store.alertFilters};
})(AlertSelector);
