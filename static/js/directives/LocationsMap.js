import * as _ from 'lodash'
import * as d3 from 'd3';
require('js-marker-clusterer/src/markerclusterer')

let template = `
    <div
        style="position:relative;
        padding-bottom:40%;"
    >
        <div id="locationmap" style="position:absolute; top:0; right:0; bottom:0; left:0; width:100%; height:100%;" ></div>
        
        <!--<ng-map style="position:absolute; top:0; left:0; bottom:0; right:0; width:100%; height: 100%;"-->
                <!--center="46.8815115,9.1133242"-->
                <!--zoom="4"-->
        <!--&gt;-->
            <!--<marker-->
                <!--position="{$ place.lat $},{$ place.long $}"-->
                <!--ng-repeat="place in places"-->
                <!--icon="{ url:'/static/images/user_pin.png', scaledSize:[30,30]} "-->
            <!--&gt;</marker>-->
            <!---->
            <!--<marker-->
                <!--ng-repeat="les in leslist"-->
                <!--icon="{ url:'/static/images/les_pin.png', scaledSize:[30,30]} "-->
                <!--position="{$ les.lat+','+les.long $}"-->
            <!--&gt;-->
            <!--<info-window>Ciao</info-window>-->
            <!--</marker>-->
        <!--</ng-map>-->

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
                    styles : mapStyles
                });
    
                console.log('Map : ', map)
                
                // NgMap.getMap().then((map) => {
                    
                    // markers = _.map($scope.places , place=> {
                    //     return new google.maps.Marker({
                    //         position: new google.maps.LatLng(place.lat,place.long),
                    //         title: 'test',
                    //         icon:{ url:'/static/images/user_pin.png'}
                    //         icon:{ url:'/static/images/user_pin.png', size: [100, 100], scaledSize:[20,20]}
                    //     });
                    // })
                    //
                
                    let markers = _.map($scope.places.concat($scope.leslist) , place=> {
                        
                        return new google.maps.Marker({
                            position: new google.maps.LatLng(place.lat,place.long),
                            icon:{ url: place.is_less ? '/static/images/les_pin.png' :'/static/images/user_pin.png' , scaledSize: new google.maps.Size(35,35) }
                        })
                        
                        
                    })
                
                    let cluster = new MarkerClusterer(map, markers, { imagePath: '/static/images/markers/m'});
                    
                    console.log('cluster :' , cluster )
                    
                // });
    
                // $scope.createMarkerForCity = function (city) {
                //
                //     var marker = new google.maps.Marker({
                //         position: new google.maps.LatLng(city.lat, city.long),
                //         title: city.name,
                //         icon:{ url:'/static/images/user_pin.png', scaledSize:[20,20]}
                //     });
                //
                //     // google.maps.event.addListener(marker, 'click', function () {
                //     //     $scope.selectedCity = city;
                //     //     $scope.map.showInfoWindow('myInfoWindow', this);
                //     // });
                //     return marker;
                // }
    
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
                "saturation": -100
            },
            {
                "lightness": 65
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
                "hue": "#efefef"
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