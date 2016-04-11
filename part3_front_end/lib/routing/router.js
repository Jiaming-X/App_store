/**
 * Created by jiamingxie on 4/11/16.
 */
Router.configure({
    layoutTemplate: "masterLayout"
});

Router.route('/', {
    name: 'topChart',
    waitOn: function() {
        Meteor.subscribe('apps', {sort: {numberOfRecommendations: -1, avgRating: -1}, limit: 50});
    },
    data: function () {
        return {
            apps: Apps.find({}, {sort: {numberOfRecommendations: -1, avgRating: -1}, limit: 50})
        };
    }
});

Router.route('/app/:_id', {
    name: 'appPage',
    waitOn: function() {
        Meteor.subscribe('singleApp', this.params._id);
    },
    data: function () {
        return Apps.findOne(this.params._id);
    }
});
