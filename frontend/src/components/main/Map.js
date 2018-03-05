/**
 * Created by jasonjohns on 6/16/17.
 */

import React, {Component} from 'react';
import ReactMapboxGL, {Cluster, Marker} from 'react-mapbox-gl';

import {Institution, MAPBOX_API_TOKEN} from './../../agent';

import './map.css';

const Map = ReactMapboxGL({accessToken: MAPBOX_API_TOKEN});

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
            data: []
            
        };
        
        
    }
    
    transformData(data) {
        let transformed = [];
        
        data.forEach(e => {
            transformed.push({
                lat: e.location.latitude,
                lng: e.location.longitude,
                options: {
                    title: e.name,
                    web: e.web_address
                }
            });
        });
        
        console.log(`Transformed ${transformed.length} of ${data.length} records`);
        return transformed;
    }
    
    componentDidMount() {
        console.info('Starting request for geo data');
        const req = Institution.getAllGeo();
        
        req
            .then(data => {
                console.info('Received institution geo data');
                console.log(data);
                this.setState({
                    data: this.transformData(data)
                })
            })
            .catch(err => {
                console.error('Error retrieving institution geo data');
                console.error(err);
            })
    }
    
    clusterMarker = (coordinates, pointCount) => (
        <Marker
            coordinates={coordinates}
            className="clusterMarker">
            <div>{pointCount}</div>
        </Marker>
    );

    onMarkerClick(e, location){
        console.log(e);
        console.log(location);
    }

    shouldComponentUpdate(nextProps, nextState) {
        return this.state.data !== nextState.data;
    }

    render() {
        return(
            <Map
                style={this.state.mapStyle}
                containerStyle={this.state.viewport.containerStyle}
                center={this.state.viewport.center}
                zoom={this.state.viewport.zoom}
                log={true}
            >
                <Cluster ClusterMarkerFactory={this.clusterMarker}
                         log={true}
                         clusterThreshold={64}
                >
                    {
                        this.state.data.map((location, key) => {
                            if (this.state.data.length === 0)
                                return null;

                           return <Marker
                                key = {key}
                                coordinates = {[location.lng, location.lat]}
                                className = "marker"
                                onClick = {this.onMarkerClick.bind(this, location)}
                            />
                        })
                    }
                </Cluster>
            
            </Map>
        )
    }
}

export default ApplicationMap;