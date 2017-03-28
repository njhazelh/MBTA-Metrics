import React from 'react';
import { Row, Col, Input, Form, Label } from 'reactstrap';

export default class LineSelector extends React.Component {
  render() {
    let lines = ['FAI', 'FIT', 'FRG', 'FRK', 'GRE', 'HAV', 'KIG', 'LOW', 'MID', 'NEE', 'NEW', 'PRO'];
    return (
      <fieldset>
        <legend>Lines</legend>
        <Form>
          <Row  className='ml-15'>
            <Col xs={4}>
              <Input type='checkbox' name='all'/>
              <Label for='all'>Select All</Label>
            </Col>
            <Col xs={8}>
              <Row>
                {
                  lines.map(line =>
                    <Col xs={3} key={line}>
                      <Input type='checkbox' name={line}/>
                      <Label for={line}>{line}</Label>
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
