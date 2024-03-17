import COLORS from "../constants/COLORS";

export const SimplePieChartOption = (title, dataArr) => {
    return {
        title: {
            text: title, // Main title text
            left: 'Left', // Position the title in the center
            textStyle: {
                color: COLORS.primary, // Title color
                fontWeight: 'bold', // Make the title font bold
                fontSize: 24 // Set the font size for the title
            }
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '5%',
            left: 'center'
        },
        series: [
            {
                name: { title },
                // name: 'Yearly Balance',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 40,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                grid: {
                    top: '50', // Give more room at the top
                    right: '50',
                    bottom: '50', // Provide space for rotated labels
                    left: '8%',
                    containLabel: true
                },
                data: dataArr
            }
        ]
    };
}