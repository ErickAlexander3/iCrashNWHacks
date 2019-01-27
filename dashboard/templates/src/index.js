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
    }

    render(){
      return (
        <div>
          <div>
              <div>
                  <div><p>Time Escaping</p></div>
              </div>
          </div>
          <div>
              <div>
                <div><p>Money to be Paid</p></div>
              </div>
          </div>
        </div>
      );
    }
}

  class ParkingSummary extends React.Component{
    constructor(props){
      super(props);
    }

    render() {
      return (
      <div>
          <h3>Your Parking Summary</h3>
          <BootstrapTable data={""} options={ { noDataText: 'This is custom text for empty data' } }>
              <TableHeaderColumn dataField='date' isKey={ true }>Date</TableHeaderColumn>
              <TableHeaderColumn dataField='time'>How much time you have been parking on that day</TableHeaderColumn>
              <TableHeaderColumn dataField='cost'>How much you need to pay</TableHeaderColumn>
              <TableHeaderColumn dataField='paid'>paid or click here to pay</TableHeaderColumn>
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
