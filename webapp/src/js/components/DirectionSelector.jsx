import React from 'react';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';

export default class DirectionSelector extends React.Component {
  render() {
    let directions = ['Inbound', 'Outbound'];
    return (
      <fieldset className="my-3">
        <legend>
          Directions:
          <Button outline color="primary" className="togglebutton">All</Button>
          <Button outline color="warning" className="togglebutton">None</Button>
        </legend>
        <Form>
          <Row>
            {
              directions.map(direction =>
                <Col key={direction} xs={6} md={4} lg={3}>
                  <Label check>
                    <Input type='checkbox' name={direction}/>{' '}
                    {direction}
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
