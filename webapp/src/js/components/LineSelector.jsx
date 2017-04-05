import React from 'react';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';

export default class LineSelector extends React.Component {
  render() {
    let lines = ['FAIRMOUNT', 'FITCHBURG', 'FRAMINGHAM', 'FRANKLIN', 'GREENBUSH', 'HAVERHILL', 'KINGSTON', 'LOWELL', 'MIDDLEBOROUGH', 'NEEDHAM', 'NEWBURYPORT', 'PROVIDENCE'];
    return (
      <fieldset className="my-3">
        <legend>
          Lines:
          <Button outline color="primary" className="togglebutton">All</Button>
          <Button outline color="warning" className="togglebutton">None</Button>
        </legend>
        <Form>
          <Row>
            {
              lines.map(line =>
                <Col xs={6} md={4} lg={3} key={line}>
                  <Label check style={{whiteSpace: 'nowrap'}}>
                    <Input type='checkbox' name={line}/>{' '}
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
