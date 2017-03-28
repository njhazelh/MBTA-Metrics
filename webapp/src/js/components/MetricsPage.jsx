import React from 'react';
import { connect } from 'react-redux';

import AlertSelector from './AlertSelector';
import LineSelector from './LineSelector';
import DirectionSelector from './DirectionSelector';
import Charts from './ChartsComponent';
import DateTimeSelector from './DateTimeSelector';
import AlertEventList from './AlertEventList';
import store from '../store';
import { loadActionEvents } from '../actions/alertEvent-actions';
import * as alertEventApi from '../api/alertEvents';

import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';

import { Collapse, Navbar, NavbarToggler, NavbarBrand, Nav, NavItem, NavLink } from 'reactstrap';
import { Container, Row, Col } from 'reactstrap';

import { InputGroup, Input, InputGroupAddon } from 'reactstrap';
import { ListGroup, ListGroupItem, ListGroupItemHeading, ListGroupItemText } from 'reactstrap';

import {Table} from 'reactstrap';

export default class MetricsPage extends React.Component {
  render() {
    return (
      <section>
        <Container>
          <DateTimeSelector/>
          <LineSelector/>
          <DirectionSelector/>
          <Charts/>
          <AlertSelector/>
        </Container>
        <Container className='my-3' fluid>
          <AlertEventList/>
        </Container>
      </section>
    );
  }
}
