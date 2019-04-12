function buildMetadata(track_title) {

  d3.json(`songs/${track_title}`).then(function (data) {
    let artist_name = data.map(x => x.artists)[0]
      .replace("[", "")
      .replace("]", "")
    console.log(typeof artist_name, artist_name)
    console.log('song data:' + JSON.stringify(data))
    d3.select('#tab').html('')
    let myHtmlblock = d3.select('#tab');
    myHtmlblock.append('h4').text(`${track_title} by ${artist_name}`)
    myHtmlblock.append('hr')
    

    Object.keys(data).forEach(key => {
      myHtmlblock.append('p').text(
        `
        date_pulled : ${data[key].date_pulled},
        chart rank : ${data[key].chart_rank}`)

    })
  })
}

function buildCharts(song_name) {
  console.log(song_name)
  let url = `/songs/${song_name}` // Switch to song_name to display chart
  // Values not showing up, but are being logged and set up. Need to connect data
  // to chart. 
  console.log(url)

  d3.json(url).then(function (data) {

   // date_pulled, chart_rank
   let myDates = data.map(x => x.date_pulled)
   let myRanks = data.map(x => x.chart_rank)
    // // Plotly scatter Chart
    var trace1 = {
       x: myDates,
       y: myRanks,
      type: 'scatter',
      mode: 'lines+markers'
     };
    
    //  var layout = {yaxis: {autorange: 'reversed'}};
     var layout = {
      title: {
        text:'Song on the Top 100',
        font: {
          family: 'Arial, sans-serif',
          size: 24
        },
      },
      
      xaxis: {
  
        title: {
          text: 'Days on the Top 100',
          font: {
            family: 'Arial, sans-serif',
            size: 18,
            color: '#7f7f7f'
          }
        },
      },
      
      yaxis: {
       autorange: 'reversed',
        title: {
          text: 'Top 100 Rank',
          font: {
            family: 'Arial, sans-serif',
            size: 18,
            color: '#7f7f7f'
          }
        }
      }
    
    };
     console.log(trace1)
    
    
    Plotly.newPlot('scatter', [trace1], layout);

   
  })
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/songs").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    console.log("First Sample" + firstSample)
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // recieves the ID of the person who gave the sample
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();