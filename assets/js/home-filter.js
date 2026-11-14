/* Topic filter for the home page's "All posts" list. Without JS, every post stays visible. */
(function () {
  var filter = document.querySelector('.topic-filter');
  if (!filter) return;

  var chips = filter.querySelectorAll('.topic-chip');
  var rows = document.querySelectorAll('.post-row');
  var groups = document.querySelectorAll('.year-group');

  function apply(topic) {
    chips.forEach(function (chip) {
      chip.setAttribute('aria-pressed', String(chip.dataset.topic === topic));
    });
    rows.forEach(function (row) {
      row.hidden = topic !== 'all' && row.dataset.topic !== topic;
    });
    groups.forEach(function (group) {
      group.hidden = !group.querySelector('.post-row:not([hidden])');
    });
  }

  filter.addEventListener('click', function (event) {
    var chip = event.target.closest('.topic-chip');
    if (!chip) return;
    var topic = chip.dataset.topic;
    apply(topic);
    history.replaceState(null, '', topic === 'all' ? location.pathname : '#topic-' + topic);
  });

  var match = location.hash.match(/^#topic-(.+)$/);
  var initial = match && filter.querySelector('.topic-chip[data-topic="' + CSS.escape(match[1]) + '"]');
  apply(initial ? match[1] : 'all');
  filter.hidden = false;
})();
