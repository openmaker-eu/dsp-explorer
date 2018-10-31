export default function(){
    return{
            template:`
            <div class="entity-carousel__header short background-red text-white">
                 <h4>Age Distribution</h4>
            </div>
            <br>
            <div class="block-square">
                <div style="height:100%; width:100%;">
                    <canvas style="height:100%; width:100%;" class="chart chart-bar"
                        chart-data="data" chart-labels="labels" chart-options="options" chart-colors="colors">
                    </canvas> 
                </div>
            </div>
             `,
            transclude:true,
            scope:{},
            controller: function($scope, $http){
                
                $scope.data=[10, 20, 50, 30]
                $scope.labels= ['0-30', '30-40', '40-50', '50+'];
                $scope.colors= ['#a8a6b5','#a8a6b5','#a8a6b5','#a8a6b5']
                $scope.options = {
                    animation: false,
                    responsive: true,
                    aspectratio:1,
                    mantainAspectRatio: false,
                    legend: {
                        display:true,
                        position: 'bottom',
                           
                      },
                    scales: {
                        xAxes:[{
                            barPercentage: 0.6,
                        }]
                    }             
                    
                }
                
            }
           
        }
    }