import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';

class SideNav extends React.Component{
    constructor(props){
      super(props);
    }

    render(){
      return (
        <div>
          <a href="#">
            Profile
          </a>,
          <a href="#">
            Contact Manager
          </a>
        </div>
      );
    }
}

class ProgressBar extends React.Component{
    constructor(props){
      super(props);
      this.state = {seconds:0};
    }

    tick(){
      this.setState(state => ({
        seconds: state.seconds + 1
      }));
    }

  componentDidMount() {
    this.interval = setInterval(() => this.tick(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
  }

    render(){

      return (
        <div>
          <div>
              <div>
                  <div><p> {this.state.seconds} s</p></div>
              </div>
          </div>
          <div>
              <div>
                <div><p>30 CAD</p></div>
              </div>
          </div>
        </div>
      );
    }
}

  class ParkingSummary extends React.Component{
    constructor(props){
      super(props);
      // this.state = {var myData = JSON.parse(myjsonstring)};
    }

    

    render() {
      return (
      <div>
          <h3>Your Parking Summary</h3>
          <BootstrapTable>
              <TableHeaderColumn dataField='date' isKey={ true }>2019-01-26</TableHeaderColumn>
              <TableHeaderColumn dataField='time'> 2 hours of parking </TableHeaderColumn>
              <TableHeaderColumn dataField='cost'>60 CAD</TableHeaderColumn>
              <TableHeaderColumn dataField='lotNum'>at Parking #123</TableHeaderColumn>
              <TableHeaderColumn dataField='paid'><button>paid or click here to pay</button></TableHeaderColumn>
          </BootstrapTable>
        </div>
      );
   }
  }

// ========================================

ReactDOM.render(
  <SideNav />,
  document.getElementById('roots')
);

ReactDOM.render(
  <ProgressBar />,
  document.getElementById('pb-roots')
);

ReactDOM.render(
  <ParkingSummary />,
  document.getElementById('sum-roots')
);
