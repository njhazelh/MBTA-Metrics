import React from 'react';
import { Container, Row, Col, Form, FormGroup, Input, Label } from 'reactstrap';

export default class DateTimeSelector extends React.Component {
  render() {
    return (
      <div>
        <Row className='my-3'>
          <Col>
            <fieldset>
              <legend>Date Range</legend>
              <Form inline>
                <FormGroup>
                  <Label for='from_date' className='mr-2'>From</Label>
                  <Input type='date' name='from_date' placeholder="date placeholder"/>
                </FormGroup>
                <FormGroup>
                  <Label for='to_date' className='mx-2'>to</Label>
                  <Input type='date' name='to_date' placeholder="date placeholder"/>
                </FormGroup>
              </Form>
            </fieldset>
          </Col>
        </Row>
        <Row className='my-3'>
          <Col>
            <fieldset>
              <legend>Time Range</legend>
              <Form inline>
                <FormGroup>
                  <Label for='from_time' className='mr-2'>From</Label>
                  <Input type='time' name='from_time'/>
                </FormGroup>
                <FormGroup>
                  <Label for='to_time' className='mx-2'>to</Label>
                  <Input type='time' name='to_time'/>
                </FormGroup>
              </Form>
            </fieldset>
          </Col>
        </Row>
      </div>
    );
  }
}
