import * as _ from 'lodash'
import * as d3 from 'd3';
require('js-marker-clusterer/src/markerclusterer')

let template = `
    <div style="position:relative; padding-bottom:40%;" >
        <div id="locationmap" style="position:absolute; top:0; right:0; bottom:0; left:0; width:100%; height:100%;" ></div>
    </div>
`
export default [function(){
    
    return {
        template:template,
        controller : ['$scope','$http', '$element', 'NgMap', function($scope, $http, $element, NgMap){
            $scope.places=[]
            $scope.leslist=[
                { lat:'43.2633182', long:'-2.9685838', city:'Bilbao' , is_less:true  },
                { lat:'48.1356952', long:'16.9758341', city:'Bratislava' , is_less:true  },
                { lat:'43.7799528', long:'11.2059486', city:'Firenze' , is_less:true  },
                { lat:'52.4774169', long:'-1.9336706', city:'Birmingham' , is_less:true  },
                { lat:'53.4121569', long:'-2.9860978', city:'Liverpool' , is_less:true  },
                { lat:'53.4916393', long:'-2.3231298', city:'Salford' , is_less:true  },
                { lat:'45.0544696', long:'7.6617633', city:'Torino' , is_less:true  },
                { lat:'43.7799528', long:'11.2059486', city:'Firenze' , is_less:true  },
                { lat:'53.472225', long:'-2.2935019', city:'Manchester' , is_less:true  },
                { lat:'51.5285582', long:'-0.2416795', city:'Londra', is_less:true   }
            ]
    
            $http.get('/api/v1.1/get_places').then( (results)=>{
                
                $scope.places = _.map( results.data.places, e => JSON.parse(e) )
    
                var map = new google.maps.Map(document.getElementById('locationmap'), {
                    zoom: 4,
                    center: new google.maps.LatLng(46.8815115,9.1133242),
                    styles : mapStyles,
                    streetViewControl: false
                });
                
                let markers = _.map($scope.places.concat($scope.leslist) , place=> {
                    
                    return new google.maps.Marker({
                        position: new google.maps.LatLng(place.lat,place.long),
                        icon:{
                            url: place.is_less? '/static/images/markers/les_pin.png' : '/static/images/markers/user_pin.png' ,
                            // size: new google.maps.Size(30,35)
                            // ,
                            scaledSize: new google.maps.Size(35,35)
                        }
                    })
                    
                    
                })
                
                let cluster = new MarkerClusterer(map, markers, { imagePath: '/static/images/markers/m'});
                map.panTo(map.getCenter());
            })
            
            
        }]
    }
    
}]

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