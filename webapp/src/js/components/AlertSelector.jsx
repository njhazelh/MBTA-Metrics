import React from 'react';
import { Row, Col, Label, Input, Form, Button } from 'reactstrap';

export default class AlertSelector extends React.Component {
  render() {
    let alerts = ['Existent', 'Nonexistent', 'Timely', 'Late', 'Accurate','Innaccurate'];
    return (
        <fieldset className="my-3">
          <legend>
            Alerts:
            <Button outline color="primary" className="togglebutton">All</Button>
            <Button outline color="warning" className="togglebutton">None</Button>
          </legend>
          <Form>
            <Row>
              {
                alerts.map(alert =>
                  <Col xs={6} key={alert}>
                    <Label check>
                      <Input type='checkbox' name={alert}/>{' '}
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
