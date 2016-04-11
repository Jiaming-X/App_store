/**
 * Created by jiamingxie on 4/11/16.
 */
if(Apps.find({}).count() < 1){

    var fs = Npm.require('fs');

    fs.readFile('../../../../../server/data.json', 'utf8', Meteor.bindEnvironment(function(err, data) {
        if (err) throw err;
        var newAppData = data.split("\n");

        for (var i = 0; i < newAppData.length - 1; i++) {
            var rawAppData = JSON.parse(newAppData[i]);
            var newApp = {};

            newApp.name = rawAppData.title;
            newApp.app_id = rawAppData.app_id;
            newApp.developer = rawAppData.developer;
            newApp.description = rawAppData.intro;
            newApp.avgRating = parseInt(rawAppData.score) / 2;
            newApp.iconUrl = rawAppData.thumbnail_url;
            newApp.reccomendedApps = rawAppData.top_5_app;
            newApp.numberOfRecommendations = 0;

            Apps.insert(newApp);
        }

        var cursor = Apps.find();
        cursor.map(function(one_app){
            var recommended_apps = one_app.reccomendedApps;

            if(recommended_apps){
                var len = recommended_apps.length;
                for (var i = 0; i < len; i++) {
                    Apps.update({
                        app_id: String(recommended_apps[i])
                    }, {
                        $inc: {
                            numberOfRecommendations: 1
                        }
                    });
                }
            }
        });
    }, function(err){
        throw err;
    }));
}
