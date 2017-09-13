import * as _ from 'lodash'
import * as d3 from 'd3';

let template = `
    <div map-lazy-load="https://maps.google.com/maps/api/js"
         style="position:relative;
         padding-bottom:40%;">
        <ng-map style="position:absolute; top:0; left:0; bottom:0; right:0; width:100%; height: 100%;"
                center="46.8815115,9.1133242"
                zoom="4"
        >
            <marker
                position="{$ place.lat $},{$ place.long $}"
                ng-repeat="place in places"
                icon="{ url:'/static/images/user_pin.png', scaledSize:[30,30]} "
            ></marker>
            
            <marker
                ng-repeat="les in leslist"
                icon="{ url:'/static/images/les_pin.png', scaledSize:[30,30]} "
                position="{$ les.lat+','+les.long $}"
            >
            <info-window>Ciao</info-window>
            </marker>
            
            
        </ng-map>

    </div>
`

export default [function(){
    
    return {
        template:template,
        controller : ['$scope','$http', 'NgMap', function($scope, $http, NgMap){
            $scope.places=[]
            $scope.leslist=[
                { lat:'43.2633182', long:'-2.9685838', city:'Bilbao' },
                { lat:'48.1356952', long:'16.9758341', city:'Bratislava' },
                { lat:'43.7799528', long:'11.2059486', city:'Firenze' },
                { lat:'52.4774169', long:'-1.9336706', city:'Birmingham' },
                { lat:'53.4121569', long:'-2.9860978', city:'Liverpool' },
                { lat:'53.4916393', long:'-2.3231298', city:'Salford' },
                { lat:'45.0734673', long:'7.6055672', city:'Torino' },
                { lat:'43.7799528', long:'11.2059486', city:'Firenze' },
                { lat:'53.472225', long:'-2.2935019', city:'Manchester' },
                { lat:'51.5285582', long:'-0.2416795', city:'Londra' }
            ]
            
            $http.get('/api/v1.1/get_places').then( (results)=>{
                $scope.places = _.map( results.data.places, e => JSON.parse(e) )
                console.log('Results :', $scope.places)
            })
    
            // NgMap.getMap().then(function (map) {
            //     $scope.map = map;
            //     $scope.initMarkerClusterer();
            // });
            //
            // $scope.initMarkerClusterer = function () {
            //     var markers = $scope.places.map(function (city) { return $scope.createMarkerForCity(city);
            //     });
            //     var mcOptions = { imagePath: 'https://cdn.rawgit.com/googlemaps/js-marker-clusterer/gh-pages/images/m' };
            //     return new MarkerClusterer($scope.map, markers, mcOptions);
            // };
            //
            // $scope.createMarkerForCity = function (city) {
            //     var marker = new google.maps.Marker({
            //         position: new google.maps.LatLng(city.pos[0], city.pos[1]),
            //         title: city.name,
            //         icon:{ url:'/static/images/user_pin.png', scaledSize:[20,20]}
            //     });
            //     google.maps.event.addListener(marker, 'click', function () {
            //         $scope.selectedCity = city;
            //         $scope.map.showInfoWindow('myInfoWindow', this);
            //     });
            //     return marker;
            // }
            
            
        }]
    }
    
}]