import React from 'react';

import { Row, Col } from 'reactstrap';

import AccuracyChart from './AccuracyChart';
import ExistenceChart from './ExistenceChart';
import TimelinessChart from './TimelinessChart';

const Charts = () =>
  <Row className="mb-5 justify-content-center">
    <Col lg={4} md={6} sm={12} className="my-3"><ExistenceChart /></Col>
    <Col lg={4} md={6} sm={12} className="my-3"><TimelinessChart /></Col>
    <Col lg={4} md={6} sm={12} className="my-3"><AccuracyChart /></Col>
  </Row>;

export default Charts;
