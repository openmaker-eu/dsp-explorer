import * as _ from 'lodash'

export default [ '$scope','$http', function ($scope,$http) {

    $scope.user_message = ''
    $scope.message_history = []

    $scope.news = []
    $scope.available_articles = []

    $scope.otions = ['next', 'topics']
    $scope.answers = ['Yes', 'No', 'Dunno']
    $scope.date_options = ['yesterday', 'week', 'month']

    $scope.filter = {
        date: $scope.date_options[2],
        cursor: -1,
        topic_id: null,
        topic_name: null
    }

    let make_question_yes_or_not = false

    // random display a question
    $scope.questionOrNot = () => {
        make_question_yes_or_not = _.sample([true,false])
        if (make_question_yes_or_not) {
            // question
            let welcome_message = {
                type : 'question',
                source : 'bot',
                date: Date.now(),
                message: 'This is a sample question about something relevant?'
            }
            $scope.message_history.unshift(welcome_message)
        } else {
            // no question
            $scope.options()
        }
    }

    // welcome message
    $scope.welcome = () => {
        let welcome_message = {
            type : '',
            source : 'bot',
            date: Date.now(),
            message: 'Hi! Click on one of our topics to read related articles'
        }
        $scope.message_history.unshift(welcome_message)
        $scope.topics()
    }

    // option message
    $scope.options = () => {
        let bot_message = {
            type : 'options',
            source : 'bot',
            date: Date.now(),
            message: $scope.otions
        }
        $scope.message_history.unshift(bot_message)
    }

    $scope.contentFinished = () => {
        let finish_message = {
            type : '',
            source : 'bot',
            date: Date.now(),
            message: `Hey! You have checked all the articles about ${$scope.filter.topic_name}. Go on exploring another topic`
        }
        $scope.message_history.unshift(finish_message)
        $scope.topics()
    }

    // return list of topics
    $scope.topics = () => {
        $http({
            url: '/api/v1.2/topics/',
            method: "GET"
        }).then(
            res=>{

                let bot_message = {
                    type : 'topics',
                    source : 'bot',
                    date: Date.now(),
                    message: res.data.result.topics
                }

                $scope.message_history.unshift(bot_message)

                // every change of topic empty the news list
                $scope.news = []

            }
        )
    }

    // return news
    $scope.newsByTopic = (topic_id, topic_name) => {

        $scope.filter.topic_id = topic_id
        $scope.filter.topic_name = topic_name

        if($scope.available_articles.length) {

            let bot_message = {
                type : 'news',
                source : 'bot',
                date: Date.now(),
                message:  $scope.available_articles[0]
            }

            $scope.message_history.unshift(bot_message)

            // check if question or not
            // if question don't show next article button or topics but answers and than show next article button or topics
            // if not question show next article button or topics
            $scope.questionOrNot()

            //$scope.options()
            $scope.available_articles.shift()

        } else {
            // new search with new filters
            console.log($scope.filter.cursor)
            if ($scope.filter.cursor == 0) {$scope.contentFinished(); return}
            $http({
                url: '/api/v1.2/news/' + $scope.filter.topic_id + '/'+ $scope.filter.date +'/' + $scope.filter.cursor,
                method: "GET"
            }).then(
                res=>{

                    $scope.filter.cursor = res.data.result.next_cursor

                    // fill array
                    $scope.available_articles = $scope.available_articles.concat(res.data.result.news)

                    let bot_message = {
                        type : 'news',
                        source : 'bot',
                        date: Date.now(),
                        message: $scope.available_articles[0]
                    }

                    $scope.message_history.unshift(bot_message)

                    // check if question or not
                    // if question don't show next article button or topics but answers and than show next article button or topics
                    // if not question show next article button or topics
                    $scope.questionOrNot()

                    //$scope.options()
                    $scope.available_articles.shift()

                }
            )
        }
    }

    $scope.message = () => {

        let user_message = {
            source:'user',
            date: Date.now(),
            message: $scope.user_message
        }

        $scope.message_history.unshift(user_message)

        $http({
            url: '/chatbot/v1.1/message/',
            method: "POST",
            data: `message=${$scope.user_message}`,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        }).then(
            res=>{
                let bot_message = {
                    source : 'bot',
                    date: Date.now(),
                    message: res.data.message
                }

                $scope.message_history.unshift(bot_message)
                // $scope.json_message = res.data.nlu
                $scope.nlu_last_response = JSON.stringify(res.data, undefined, 2);
                $scope.user_message = ''
            }
        )

    }

}]