const maxApi = require('max-api');
const googleTrendsApi = require('google-trends-api');

maxApi.addHandler('getGoogleTrends', function() {
	googleTrendsApi.realTimeTrends({
		geo: 'US',
		category: 'e',
	}, function(err, results) {
		if (err) {
			maxApi.outlet('No story was found at this time. Please try again later.');
		}else{
			formattedData = JSON.parse(results);
			trendingStoryTitle = formattedData.storySummaries.trendingStories[0].articles[0].articleTitle;
			trendingStorySnippet = formattedData.storySummaries.trendingStories[0].articles[0].snippet;
			maxApi.outlet(trendingStorySnippet);
		}
	});
});