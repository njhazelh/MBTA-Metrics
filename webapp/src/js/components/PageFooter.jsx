import React from 'react';
import { Row, Col, Container } from 'reactstrap';

const PageFooter = () =>
  <footer className="footer">
    <Container>
      <Row className="justify-content-center" style={{ textAlign: 'center' }}>
        <Col xs={2}>Spring 2017</Col>
      </Row>
    </Container>
  </footer>;

export default PageFooter;
