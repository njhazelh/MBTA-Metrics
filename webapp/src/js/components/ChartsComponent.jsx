import React from 'react';

import { Row, Col } from 'reactstrap';

export default () =>
  <Row  className='my-5 justify-content-center'>
    <Col lg={4}><div style={{width:'300px', height:'300px', backgroundColor:'red', margin: '5px auto'}}>Existence</div></Col>
    <Col lg={4}><div style={{width:'300px', height:'300px', backgroundColor:'red', margin: '5px auto'}}>Timeliness</div></Col>
    <Col lg={4}><div style={{width:'300px', height:'300px', backgroundColor:'red', margin: '5px auto'}}>Accuracy</div></Col>
  </Row>;
