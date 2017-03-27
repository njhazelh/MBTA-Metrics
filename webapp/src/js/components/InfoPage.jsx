import React from 'react';
import { Container } from 'reactstrap';

export default () =>
  <Container>
    <h1>Welcome to the MTBA Alert Metrics page</h1>
    <div className='lead'>
      <p>
        This site is intended to provide
        insight into the accuracy and existence of MBTA alerts related to the
        commuter rail.
      </p>
      <p>
        Since this page is a work in progress, don't expect everything to work,
        but check-back soon, and hopefully things will be better.
      </p>
    </div>
  </Container>;
