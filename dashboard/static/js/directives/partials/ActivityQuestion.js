let fields = require('../../../templates/question_templates.html')
import {TemplateLoader} from '../../classes/TemplateLoader'

let activities = {
    domain : ['Community', 'IT', 'Manufacturing'],
    area : ['3D Modelling', '3D printing', '3D printing : BJ', '3D printing : Cladding', '3D printing : Concrete 3D printing', '3D printing : FFF', '3D printing : LOM', '3D printing : Material Jetting', '3D printing : Material Jetting', '3D printing : Printing Material', '3D printing : SLS', '3D printing: SLA', 'Collaboration', 'Collaboration : Connecting', 'Collaboration : Content communities', 'Collaboration : Online Collaborative Design Platform', 'Collaboration : Questionnaire', 'Collaboration : Source Code Management', 'Collaboration : Team Collaboration', 'Collaboration: Collaborative Design', 'Commercialization', 'Commercialization : Co Design', 'Commercialization : Funding', 'Commercialization : Sales', 'Communication', 'Communication : Social Networking Sites', 'Design', 'Design : Simulation', 'Design: Drag and Drop Production', 'Electronics', 'Electronics : DIY Electronics', 'Interaction', 'Interaction : 3D Interaction', 'Interaction : 3D Visualisation', 'Interaction : Display', 'Interaction : Input', 'Internet of things', 'Internet of things : Data analytics', 'Internet of things : Database', 'Internet of things : Visualisation', 'Learning', 'Learning : Content Communities', 'Milling', 'Modelling', 'Modelling : DIY Electronics', 'Organisation', 'Organisation : Community Tools', 'Robotics', 'Sharing', 'Sharing : Blogs', 'Sharing : Collaborative Projects', 'Sharing : Content communities', 'Sharing : Files Repository', 'Sharing : Virtual Game Worlds', 'Sharing : Virtual Social Worlds', 'Software Development', 'Software Development : Cloud Computing', 'Software Development : Programming', 'Software Development : Team Collaboration', 'Telecommunication', 'Telecommunication : Long Range', 'Telecommunication : Short Range'],
    technology : ['3D files repository', '3D modelling software', '3D printing service', '3D scanning software', '5G', 'Artificial Intelligence', 'Augmented reality', 'Blockchain Technology', 'Blog Platform', 'Bookmarking', 'Brain Computer Interface', 'Broadcasting platform', 'Business Intelligence Software', 'Cave automatic virtual environment', 'Chatbot Platform', 'Cloud Services', 'CNC - Open Source', 'CNC - Plug and Play', 'Community Discussion Forum', 'Competition Platform', 'Computer Vision', 'Crowdfunding Management', 'Customization software', 'Dataflow programming', 'Descriptive Analytics', 'Diagnostic Analytics', 'Directory', 'Distributed Computing', 'Documentation Platform', 'Domestic Robots', 'Donation Platform', 'eCommerce Website', 'Equity crowdfunding', 'Event management platform', 'FDM - Kit / DIY', 'Filament Recycling', 'Fog Computing', 'Free CAD software', 'Gamification', 'Gaming', 'Gesture Recognition', 'Graph Database', 'Grid Computing', 'Home Automation', 'IaaS', 'Image sharing platform', 'Indoor Localisation', 'Instruction platforms', 'Laser Melting Metal', 'LPWAN', 'Machine Learning', 'Maker Academies', 'Massive Open Online Course', 'Microcontroller', 'Mixed Reality', 'Nanoelectronics', 'NB-IoT', 'News Aggregation', 'News blogs', 'Online big data analytics', 'Online circuit design platform', 'Online market place', 'Online Reviews', 'Optical head-mounted display', 'Organisation search engine', 'P2P', 'P2P Lending', 'PaaS', 'Personal Networks', 'Phone AR', 'Podcast platform', 'Predictive Analytics', 'Prescriptive Analytics', 'Product Discussion Forum', 'Project Hosting platform', 'Project management platform', 'Reward crowdfunding', 'Robotic Arm', 'SaaS', 'Sensor Data Collection Platforms', 'SLS - Kit / DIY', 'SLS - Plug and Play', 'Smart Contracts', 'Smart Glasses', 'Speech Recognition', 'Survey Platform', 'Team Communication', 'Time Series Database', 'Timezone management', 'Video sharing platform', 'Virtual reality', 'Visual Programming', 'Visualisation', 'WiKi platform', 'Z-Wave', 'ZigBee'],
    skills : ['Coding: Python', 'Coding: Processing', 'Coding: Django', 'Graphic design', 'Wood carving', 'Clay Sculpting', 'Team Management', 'Workshop Coordination', 'Budgeting', 'Marketing', 'Product design', 'Creative writing', 'Lecturing', 'Painting', 'Social entrepreneurship', 'Drawing'],
}

let template = `
    <style> .activities-form .ui-select-match {font-size:80%;} </style>
    <div ng-repeat="(key,activity) in activities" class="activities-form" ng-init="data[key] || (data[key]='')">
        <label for="" class="capitalize">{$ key $}</label>
        <ui-select
            multiple
            class="form-control"
            ng-model="data[key]"
            title="Write here to search available {$ key $}"
        >
            <ui-select-match placeholder="Type to search for {$ key $}">{$ $item $}</ui-select-match>
            <ui-select-choices repeat="activ in activity | filter:$select.search track by $index">
                <!--<div ng-bind-html="tag | highlight: $select.search"></div>-->
                <div>{$ activ $}</div>
            </ui-select-choices>
        </ui-select><br/>
        <input type="hidden" ng-model="data[key]" ng-value="data[key]" name="{$ key $}" required/>
    </div>
`

export default {
    transclude: true,
    template: template,
    bindings: {
        data:'<'
    },
    controller: ['$scope', '$element', '$compile', function($scope, $element, $compile) {
    
        this.$onChanges = function (changes) {
            $scope.data = changes.data && changes.data.currentValue || undefined
            $scope.activities = activities
            // $scope.x = this.model
        
            console.log('Model', $scope.data);
        
        }
        
    }]
}
