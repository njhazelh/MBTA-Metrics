import React from 'react';

import PageHeader from './PageHeader';
import PageFooter from './PageFooter';

export default props =>
  <div className="app">
    <PageHeader/>
    { props.children }
    <PageFooter/>
  </div>;
