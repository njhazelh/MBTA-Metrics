
function lineFilter(state) {
  return item => state.lineFilters[item.route] === undefined
    || !!state.lineFilters[item.route];
}

function directionFilter(state) {
  return (item) => {
    let d = item.direction;
    if (d == null) {
      return true;
    }
    d = d.toLowerCase();
    return (d === 'inbound' && state.directionFilters.Inbound)
      || (d === 'outbound' && state.directionFilters.Outbound);
  };
}

function alertFilter(state) {
  return (item) => {
    const alertExisted = item.alert_issued;
    const alertIsTimely = item.alert_timely;
    const alertIsAccurate = item.delay_accuracy != null
      && item.delay_accuracy.toLowerCase() === 'accurate';
    const existenceFilter =
      (alertExisted && state.alertFilters.Existent)
      || (!alertExisted && state.alertFilters.Nonexistent);
    const timelyFilter =
      (alertIsTimely && state.alertFilters.Timely)
      || (!alertIsTimely && state.alertFilters.Late);
    const accuracyFilter =
      (alertIsAccurate && state.alertFilters.Accurate)
      || (!alertIsAccurate && state.alertFilters.Inaccurate);

    return existenceFilter && timelyFilter && accuracyFilter;
  };
}

export default function FilterDataReducer(state) {
  // This information is needed for the charts.
  const trainFilteredData = state.alertEvents
    .filter(lineFilter(state))
    .filter(directionFilter(state));
  // This stuff gets rendered in the Table.
  const alertFilteredData = trainFilteredData
    .filter(alertFilter(state));
  return {
    ...state,
    trainFilteredData,
    alertFilteredData,
  };
}
