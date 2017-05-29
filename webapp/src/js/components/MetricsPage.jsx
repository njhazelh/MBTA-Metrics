import React from 'react';
import { Container } from 'reactstrap';

import AlertSelector from './AlertSelector';
import LineSelector from './LineSelector';
import DirectionSelector from './DirectionSelector';
import Charts from './ChartsComponent';
import DateTimeSelector from './DateTimeSelector';
import AlertEventList from './AlertEventList';
import CSVDownloadButton from './CSVDownloadButton';

export default class MetricsPage extends React.Component {
  render() {
    return (
      <section>
        <Container>
          <DateTimeSelector />
          <LineSelector />
          <DirectionSelector />
          <Charts />
          <AlertSelector />
        </Container>
        <Container className="my-3" fluid>
          <CSVDownloadButton />
          <AlertEventList />
        </Container>
      </section>
    );
  }
}
