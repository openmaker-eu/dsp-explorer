 let _ = require('lodash')
 require('js-marker-clusterer/src/markerclusterer')

let template = `
    <div style="position:relative; padding-bottom:80%; width:100%; background: #fff;" >
        <div
            id="locationmap"
            style="position:absolute; top:0; right:0; bottom:0; left:0; width:100%; height:100%;"
        ></div>
    </div>
`

export default function(){
    return {
        template:template,
        scope: {},
        controller : ['$scope', '$rootScope', '$http', 'UserSearchFactory', '$element', function($scope, $rootScope, $http, UserSearchFactory, $element){
            
            $scope.places=[]
            $scope.leslist=[
                { lat:'48.1356952', long:'16.9758341', city:'Bratislava', is_les:true  },
                { lat:'52.4774169', long:'-1.9336706', city:'Birmingham', is_les:true  },
                { lat:'53.4121569', long:'-2.9860978', city:'Liverpool', is_les:true  },
                { lat:'53.4916393', long:'-2.3231298', city:'Salford', is_les:true  },
                { lat:'45.0652419', long:'7.6895369', city:'Torino', is_les:true  },
                { lat:'43.7799528', long:'11.2059486', city:'Firenze', is_les:true  },
                { lat:'53.472225', long:'-2.2935019', city:'Manchester', is_les:true  }
            ]
            
            const default_center = [46.8815115,9.1133242]
            
            const user_location = ()=> {
                try{
                    let loc = JSON.parse( _.get($rootScope, 'user.location').replace(/'/g, '"') )
                    return _.isEmpty(loc) ? default_center : [loc.lat, loc.long, loc.city]
                }
                catch(e){
                    console.log('[LocationMap -> user_location]', e);
                    return default_center
                }
            }
    
            const map_container = $element.find('#locationmap')[0]
            const map_center = user_location()
            
            const build_map = (results)=>{
                
                // Places list from json-string removing empty objects
                $scope.places = _(results)
                    .get('data.places')
                    .map(r=>{
                        try{ return JSON.parse(r.replace(/'/g, '"')) }
                        catch(e){return null}
                    })
                    .filter(e=>!_.isEmpty(e))
                
                console.log($scope.places);
                
                // Init map
                let map = new google.maps.Map(map_container, {
                    zoom: 5,
                    center: new google.maps.LatLng(...map_center),
                    styles : mapStyles,
                    streetViewControl: false,
                    mapTypeControl: false
                });
                
                // User Markers
                let markers = _.map($scope.places , place=> {
                    let marker = {
                        position: new google.maps.LatLng(place.lat,place.long),
                        icon:{
                            url: '/static/images/markers/user_pin.png',
                            scaledSize: new google.maps.Size(35,35)
                        },
                        om_data:place
                    }
                    return new google.maps.Marker(marker)

                })
                
                // LES markers
                let les_markers = _.map($scope.leslist, (place)=>{
                    return new google.maps.Marker( {
                        position: new google.maps.LatLng(place.lat,place.long),
                        icon:{
                            url: '/static/images/markers/les_pin.png',
                            scaledSize: new google.maps.Size(50,50),
                            labelOrigin : new google.maps.Point(25,18),
                        },
                        label: {
                            text: 'LES',
                            color: 'red',
                            fontSize: "9px",
                            fontWeight: 'bolder'
                        },
                        om_data:place,
                        map:map
                    })
    
                })
                
                // Merge all markers
                let all_markers = markers.concat(les_markers)
                
                _.each(all_markers, (m)=>{
                    google.maps.event.addListener(m, 'click', function() {
                        let city = _.get(m, 'om_data.city')
                        city && UserSearchFactory.search(city, 'city')
                    });
                })
                
                // Init Marker Clusterization
                let markercluster = new MarkerClusterer(map, markers, { imagePath: '/static/images/markers/m'});
                
                // Filter list on marker or cluster click
                google.maps.event.addListener(markercluster, "clusterclick", (cluster)=>{
                    let latlong =  _.map(cluster.getMarkers(), (e)=>{
                        return parseFloat(_.get(e, 'om_data.lat')).toFixed(6) +
                            ','+
                            parseFloat(_.get(e, 'om_data.long')).toFixed(6)
                    })

                    latlong.length > 0 && UserSearchFactory.search(_.uniq(latlong).join(';'), 'latlong', 1, 'Various locations')
                })
    
                // Set map to center
                map.panTo(map.getCenter());
                
            }

            $http.get('/api/v1.1/get_places/')
                .then(build_map)
                .catch(e=>console.log('LocationsMap error', e))
            
        }]
    }
    
}

let mapStyles = [
    
    {
        "featureType": "administrative",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#1d1d1d"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#db4348"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "administrative.province",
        "elementType": "all",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "all",
        "stylers": [
            {
                "color": "#333"
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 51
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 30
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "lightness": 40
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "all",
        "stylers": [
            {
                "saturation": -100
            },
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
            {
                "hue": "#bbb"
            },
            {
                "lightness": 0
            },
            {
                "saturation": -97
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "lightness": -25
            },
            {
                "saturation": -100
            }
        ]
    }
]
