import React from 'react';

import { Navbar, NavbarBrand, Container } from 'reactstrap';

const PageHeader = () =>
  <Navbar toggleable style={{ backgroundColor: '#a00a78', color: 'white' }}>
    <Container>
      <NavbarBrand style={{ textTransform: 'uppercase', whiteSpace: 'normal' }}>
        <h1>MBTA Commuter Rail Alerts</h1>
      </NavbarBrand>
    </Container>
  </Navbar>;

export default PageHeader;
