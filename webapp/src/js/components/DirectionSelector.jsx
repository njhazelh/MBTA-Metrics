import React from 'react';
import { Row, Col, Input, Form, Label } from 'reactstrap';

export default class DirectionSelector extends React.Component {
  render() {
    let directions = ['Inbound', 'Outbound'];
    return (
      <fieldset>
        <legend>Directions</legend>
        <Form>
          <Row className='ml-15'>
            <Col xs={4}>
              <Input type='checkbox' name='all'/>
              <Label for='all'>Select Both</Label>
            </Col>
            <Col xs={8}>
              <Row>
                {
                  directions.map(direction =>
                    <Col key={direction} xs={3}>
                      <Input type='checkbox' name={direction}/>
                      <Label for={direction}>{direction}</Label>
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
