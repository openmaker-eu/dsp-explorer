
export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white">
                 <h4>Gender Distribution</h4>
            </div>
            <br>
            <div class="block-square" ng-if="loading==false">
                <div style="height:100%; width:100%;">
                    <canvas style="height:100%; width:100%;" class="chart chart-doughnut"
                        chart-data="data" chart-labels="labels" chart-options="options" chart-colors="colors">
                    </canvas> 
                </div>
            </div>
             `,
            transclude:true,
            scope:{
                female:"=",
                male:"=",
                other:"="               
            },
            controller: function($scope, $http){
                $scope.loading=true
                $scope.genderdata= {
                    female: 10,
                    male: 5,
                    other: 1
                }
                
                $scope.AskServer = function(){
                    var ads = $http.get('/api/v1.4/stats/gender_distribution/')
                    ads.then(
                    function(success){ 
                        $scope.genderdata = success.data; 
                        console.log($scope.genderdata)
                        console.log($scope.genderdata.female)
                        $scope.loading=false
                        $scope.data=[$scope.genderdata.female, $scope.genderdata.male, $scope.genderdata.other]
                        },
                    function(error){ console.log("ritenta");$scope.loading=false
                        }
                    )
                }
                $scope.AskServer();
                $scope.labels= ['female', 'male', 'other'];
                $scope.colors= ['#d2d2d2','#a8a6b5','#f2bdc1']
                //$scope.data=[60, 30, 10]
                $scope.options = {
                    cutoutPercentage: 40,
                    animation: false,
                    responsive: true,
                    aspectratio:1,
                    mantainAspectRatio: false,
                    legend: {
                        display:true,
                        position: 'right'
                    },
                           
                }
                
            }
           
        }
    }