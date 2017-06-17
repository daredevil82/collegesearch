/**
 * Created by jasonjohns on 6/16/17.
 */

import React, {Component} from 'react';
import ReactMapboxGL, {Layer, Feature} from 'react-mapbox-gl';

import {Institution, MAPBOX_API_TOKEN} from './../../agent';

import './../../../node_modules/leaflet/dist/leaflet.css';

class ApplicationMap extends Component {
    constructor(props) {
        super(props);
        
        this.osmMapProps= {
            url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        };
        
        this.state = {
            viewport: {
                center: [-95.098, 38.531],
                bearing: 0,
                pitch: 0,
                zoom: [4],
                containerStyle: {
                    height: '100vh',
                    width: '100vw'
                }
            },
            mapStyle: "mapbox://styles/mapbox/traffic-day-v2",
            
        }
    }
    
    componentDidMount() {
        const req = Institution.getAllGeo();
        
        req
            .then(data => {
                console.log('Received institution geo data');
                console.log(data);
                this.setState({
                    data: data
                })
            })
            .catch(err => {
                console.error('Error retrieving institution geo data');
                console.error(err);
            })
    }
    
    render() {
        return(
            <ReactMapboxGL
                style={this.state.mapStyle}
                accessToken={MAPBOX_API_TOKEN}
                containerStyle={this.state.viewport.containerStyle}
                center={this.state.viewport.center}
                zoom={this.state.viewport.zoom}
            >
                <Layer
                    type="symbol"
                    id="marker"
                    layout={{ "icon-image": "marker-15" }}
                >
                </Layer>
            </ReactMapboxGL>
        )
    }
}

export default ApplicationMap;