
export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white" ng-if="loading==false">
                 <h4>Gender Distribution</h4>
            </div>
            <br>
                <!--<div class="block-square" ng-if="loading==false"> -->
            <div ng-if="loading==false">
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
            controller: ['$scope', '$http', function($scope, $http){
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
                        $scope.loading=false
                        $scope.data=[$scope.genderdata.female, $scope.genderdata.male, $scope.genderdata.other]
                        },
                    function(error){ console.log("ritenta");$scope.loading=false
                        }
                    )
                }
                $scope.AskServer();
                $scope.labels= ['female', 'male', 'other'];
                // $scope.colors= ['#d2d2d2','#a8a6b5','#f2bdc1'];
                $scope.colors= [
                    {
                        backgroundColor: 'rgba(105, 105, 105, 1)',
                        pointBackgroundColor: '#d2d2d2',
                        
                    },
                    {
                        backgroundColor: 'rgba(80, 78, 94, 1)',
                        pointBackgroundColor: '#a8a6b5',
                    
                    },
                    {
                        backgroundColor: 'rgba(227, 121, 129, 1)',
                        pointBackgroundColor: '#f2bdc1',
                      
                    }
                ]
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
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItems, data) {
                                var i, label = [], l = data.datasets.length;
                                for (i = 0; i < l; i += 1) {
                                    label[i] = $scope.labels[tooltipItems.index] + ' : ' + data.datasets[i].data[tooltipItems.index]+ '%';
                                }
                                return label;
                            }
                           
                        }
                
                    },
                }
                
            }]
        }
    }
    
