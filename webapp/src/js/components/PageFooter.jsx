import React from 'react';
import { Link } from 'react-router';
import { Row, Col, Container } from 'reactstrap';

export default () =>
  <footer className='footer'>
    <Container>
      <Row className='justify-content-center' style={{textAlign:'center'}}>
        <Col xs={2}>Spring 2017</Col>
      </Row>
      <Row className='justify-content-center' style={{textAlign:'center'}}>
        <Col md={2}>
          <Link to='/'>Home</Link>
        </Col>
        <Col md={2}>
          <Link to='info'>Info</Link>
        </Col>
      </Row>
    </Container>
  </footer>;
