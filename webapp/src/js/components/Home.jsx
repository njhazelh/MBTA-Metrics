import React from 'react';

import PageHeader from './PageHeader';
import PageFooter from './PageFooter';

const home = props =>
  <div className="app" style={{ minWidth: 320 }}>
    <PageHeader />
    { props.children }
    <PageFooter />
  </div>;

export default home;
