import React from 'react';

import { Navbar, NavbarBrand, Container } from 'reactstrap';

export default () =>
  <Navbar toggleable  style={{backgroundColor: "#a00a78", color: 'white'}}>
    <Container>
      <NavbarBrand style={{textTransform:'uppercase', whiteSpace:"normal"}}><h1>MBTA Commuter Rail Alerts</h1></NavbarBrand>
      <div style={{color: 'yellow'}}>MOCK DATA</div>
    </Container>
  </Navbar>;
