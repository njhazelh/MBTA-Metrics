import React from 'react';
import { Link } from 'react-router';

export default class Home extends React.Component {
    render() {
        return (
          <div className="app">
            <nav className="navbar navbar-inverse bg-inverse navbar-static-top">
              <div className='container'>
                <div className='navbar-header'>
                  <Link className='navbar-brand' to="/">MBTA</Link>
                </div>
                <ul className='nav navbar-nav'>
                  <li><Link to="/list">List</Link></li>
                </ul>
                <span style={{
                  color: 'red',
                  float: 'right',
                  margin: '15px 0'
                }}>MOCK DATA</span>
              </div>
            </nav>
            <section className='container'>
              { this.props.children }
            </section>
            <footer style={{
              position: 'absolute',
              bottom: 0,
              width: '100%',
              height: '60px',
              lineHeight: '60px',
              backgroundColor: '#aaa',
              textAlign: 'center',
            }} className='container'>
              <span>
                Spring 2017.
              </span>
            </footer>
          </div>
        );
      }
}


Home.propTypes = {
    children: React.PropTypes.node,
};

Home.defaultProps = {
    children: [],
};
