
let template = /*html*/`
    <div class="container" style="font-size:120%;">
      <div class="row">
        <div id="col-md-12">
            <h1 class="text-center">Welcome to Open Maker</h1> <br>
            <p>A digital environment to collaborate, share skills, ideas and knowledge and work together on projects,
            allowing members to increase both their social impact and economic success.
            The Platform brings the Maker community online, allowing it grow and develop without losing the
            collaborative mind-set and trust-based connections that make it so unique.
            </p>
            
            <br>
            <p>
            Thanks to data-harvesting and machine learning processes, Open Maker is a smart environment and
            a living tool, that can enable members to:</p>
            <ul>
            <li>- Find and connect with other members based on the same or complementary
            preferences, skills and values;</li>
            <li>- Form valuable relationships, signal ad-hoc opportunities and partnerships, and actively
            work together on specific projects and challenges;</li>
            <li>- Get tailored information about articles to read, events to attend or influencers to follow
            </li>
            </ul>
            
            <br>
            <p>Open Maker builds on members’ concrete needs and values and brings them together in a
            community-building process.</p>
            <p>Whether you are:</p>
            <ul>
            <li>- a maker, an entrepreneur or an innovator,</li>
            <li>- someone who works in the manufacturing industry,</li>
            <li>- an academic interested in innovation, values or collaboration patters,</li>
            <li>- a policymaker thinking about the next policy instruments</li>
            <li>- a student</li>
            <li>- or simply someone passionate about new technologies and keen on social impact,</li>
            </ul>
            <p>you should register to make a difference.</p>
            Ready?
            
            <br><br>
            
            <p><small style="font-style: italic; font-weight: bold;">
            The openmaker project
            The OpenMaker project is a Horizon 2020 funded project that aims to create atransformational and collaborative
            ecosystem that fosters collective innovations within the European manufacturing sector and drives it towards more sustainable
            business models, production processes and governance systems in line with the open-source approach and socially-oriented
            spirit of the Maker Movement.
            If you have questions about the platform, you can email info@openmaker.eu
            </small></p>
        
        </div>
      </div>
    </div>
`

export default [function(){ 
    return {
        template:template,
        scope: {},
        controller : ['$scope', '$rootScope', function($scope, $rootScope) {

        }]
    }
}]
