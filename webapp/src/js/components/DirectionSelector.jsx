import React from 'react';
import { connect } from 'react-redux';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';
import store from '../store';
import * as filterActions from '../actions/filterActions';
import { DIRECTIONS } from '../constants';


class DirectionSelector extends React.Component {
  static selectAll() {
    store.dispatch(filterActions.setAllDirectionFilters(true));
  }

  static resetAll() {
    store.dispatch(filterActions.setAllDirectionFilters(false));
  }

  static setDirectionFilter(e) {
    const { value, checked } = e.target;
    store.dispatch(filterActions.setDirectionFilter(value, checked));
  }

  constructor() {
    super();
    DirectionSelector.selectAll();
  }

  render() {
    const { filters } = this.props;
    return (
      <fieldset className="my-3">
        <legend>
          Directions:
          <Button
            outline
            color="primary"
            className="togglebutton"
            onClick={DirectionSelector.selectAll}
          >
            All
          </Button>
          <Button
            outline
            color="warning"
            className="togglebutton"
            onClick={DirectionSelector.resetAll}
          >
            None
          </Button>
        </legend>
        <Form>
          <Row>
            {
              DIRECTIONS.map(dir =>
                <Col key={dir} xs={6} md={4} lg={3}>
                  <Label check>
                    <Input
                      type="checkbox"
                      name={dir}
                      value={dir}
                      // !! for undefined -> false
                      // This makes sure that the component is always controlled.
                      checked={!!filters[dir]}
                      onChange={DirectionSelector.setDirectionFilter}
                    />
                    {' '}
                    {dir}
                  </Label>
                </Col>,
              )
            }
          </Row>
        </Form>
      </fieldset>
    );
  }
}

export default connect(data => ({ filters: data.directionFilters }))(DirectionSelector);
