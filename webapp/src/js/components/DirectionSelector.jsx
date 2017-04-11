import React from 'react';
import { connect } from 'react-redux';
import { Row, Col, Input, Form, Label, Button } from 'reactstrap';
import store from '../store';
import * as filterActions from '../actions/filterActions';
import { DIRECTIONS } from '../constants';


class DirectionSelector extends React.Component {
  selectAll() {
    DIRECTIONS.forEach(direction =>
      store.dispatch(filterActions.setDirectionFilter(direction, true)));
  }

  resetAll() {
    DIRECTIONS.forEach(direction =>
      store.dispatch(filterActions.setDirectionFilter(direction, false)));
  }

  setDirectionFilter(e) {
    const { value, checked } = e.target;
    store.dispatch(filterActions.setDirectionFilter(value, checked));
  }

  render() {
    const {filters} = this.props;
    console.log(filters);
    return (
      <fieldset className="my-3">
        <legend>
          Directions:
          <Button
            outline
            color="primary"
            className="togglebutton"
            onClick={this.selectAll} >
            All
          </Button>
          <Button
            outline
            color="warning"
            className="togglebutton"
            onClick={this.resetAll} >
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
                      type='checkbox'
                      name={dir}
                      value={dir}
                      // !! for undefined -> false
                      // This makes sure that the component is always controlled.
                      checked={!!filters[dir]}
                      onChange={this.setDirectionFilter} />
                    {' '}
                    {dir}
                  </Label>
                </Col>
              )
            }
          </Row>
        </Form>
      </fieldset>
    );
  }
}

export default connect(store => {
  return {filters: store.directionFilters};
})(DirectionSelector);
