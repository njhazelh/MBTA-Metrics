import React from 'react';
import { Row, Col, Label, Input, Form } from 'reactstrap';

export default class AlertSelector extends React.Component {
  render() {
    let alerts = ['Existent', 'Timely', 'Accurate', 'Nonexistent', 'Late', 'Innaccurate'];
    return (
        <fieldset>
          <legend>Alerts</legend>
          <Form>
            <Row  className='ml-15'>
              <Col xs={4}>
                <Input type='checkbox' name='all'/>
                <Label for='all'>Select All</Label>
              </Col>
              <Col xs={8}>
                <Row>
                  {
                    alerts.map(alert =>
                      <Col xs={4} key={alert}>
                        <Input type='checkbox' name={alert}/>
                        <Label for={alert}>{alert}</Label>
                      </Col>
                    )
                  }
                </Row>
              </Col>
            </Row>
          </Form>
        </fieldset>
    );
  }
}
