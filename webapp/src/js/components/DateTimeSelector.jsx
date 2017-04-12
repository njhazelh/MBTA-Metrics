import React from 'react';
import { connect } from 'react-redux';
import { Row, Col, Form, FormGroup, Input, Label, Button } from 'reactstrap';

import store from '../store';
import { FROM_DATE, TO_DATE, FROM_TIME, TO_TIME } from '../constants';
import * as alertEventApi from '../api/alertEvents';
import * as filterActions from '../actions/filterActions';

class DateTimeSelector extends React.Component {

  static handleChange(e) {
    const { name, value } = e.target;
    store.dispatch(filterActions.setDateTimeFilter(name, value));
  }

  getValue(aspect) {
    return this.props.filters[aspect] || '';
  }

  areFieldsSet() {
    const { fromDate, toDate, fromTime, toTime } = this.props.filters;
    return !(fromDate && toDate && fromTime && toTime);
  }

  loadData() {
    const { fromDate, toDate, fromTime, toTime } = this.props.filters;
    alertEventApi.getAlertEvents(
      fromDate, toDate,
      fromTime, toTime,
    );
  }

  render() {
    return (
      <div>
        <Row className="my-3">
          <Col>
            <fieldset>
              <legend>Date Range</legend>
              <Form inline>
                <FormGroup>
                  <Label for={FROM_DATE} className="mr-2">From</Label>
                  <Input
                    type="date"
                    name={FROM_DATE}
                    value={this.getValue(FROM_DATE)}
                    onChange={DateTimeSelector.handleChange}
                    style={{
                      minWidth: 200,
                    }}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for={TO_DATE} className="mx-2">to</Label>
                  <Input
                    type="date"
                    name={TO_DATE}
                    value={this.getValue(TO_DATE)}
                    onChange={DateTimeSelector.handleChange}
                    style={{
                      minWidth: 200,
                    }}
                  />
                </FormGroup>
              </Form>
            </fieldset>
          </Col>
        </Row>
        <Row className="my-3">
          <Col>
            <fieldset>
              <legend>Time Range</legend>
              <Form inline>
                <FormGroup>
                  <Label for={FROM_TIME} className="mr-2">From</Label>
                  <Input
                    type="time"
                    name={FROM_TIME}
                    value={this.getValue(FROM_TIME)}
                    onChange={DateTimeSelector.handleChange}
                    style={{
                      minWidth: 200,
                    }}
                  />
                </FormGroup>
                <FormGroup>
                  <Label for={TO_TIME} className="mx-2">to</Label>
                  <Input
                    type="time"
                    name={TO_TIME}
                    value={this.getValue(TO_TIME)}
                    onChange={DateTimeSelector.handleChange}
                    style={{
                      minWidth: 200,
                    }}
                  />
                </FormGroup>
              </Form>
            </fieldset>
          </Col>
        </Row>
        <Row className="my-3">
          <Col>
            <Button
              color="primary"
              onClick={() => this.loadData()}
              disabled={this.areFieldsSet()}
            >
              Load Data
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}


export default connect(data => ({ filters: data.dateTimeFilters }))(DateTimeSelector);
