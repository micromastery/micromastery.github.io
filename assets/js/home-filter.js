/* Home page behaviour. Without JS, every post stays visible and Featured is a plain scrollable row. */
(function () {
  /* Topic filter for "All posts" */
  var filter = document.querySelector('.topic-filter');
  if (filter) {
    var chips = filter.querySelectorAll('.topic-chip');
    var rows = document.querySelectorAll('.post-row');
    var groups = document.querySelectorAll('.year-group');

    var apply = function (topic) {
      chips.forEach(function (chip) {
        chip.setAttribute('aria-pressed', String(chip.dataset.topic === topic));
      });
      rows.forEach(function (row) {
        row.hidden = topic !== 'all' && row.dataset.topic !== topic;
      });
      groups.forEach(function (group) {
        var count = group.querySelectorAll('.post-row:not([hidden])').length;
        group.hidden = count === 0;
        var label = group.querySelector('.year-count');
        if (label) label.textContent = count + (count === 1 ? ' post' : ' posts');
      });
    };

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
  }

  /* Dots under the swipeable Featured row (phones) */
  var track = document.querySelector('.featured');
  var dotsBox = document.querySelector('.featured-dots');
  if (track && dotsBox) {
    var cards = track.querySelectorAll('.post-card');
    cards.forEach(function (card, index) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'featured-dot';
      dot.setAttribute('aria-label', 'Show featured post ' + (index + 1));
      dot.addEventListener('click', function () {
        track.scrollTo({ left: card.offsetLeft - track.offsetLeft - parseFloat(getComputedStyle(track).paddingLeft), behavior: 'smooth' });
      });
      dotsBox.appendChild(dot);
    });
    dotsBox.removeAttribute('aria-hidden');

    var dots = dotsBox.querySelectorAll('.featured-dot');
    var update = function () {
      var active = 0;
      var best = Infinity;
      var trackLeft = track.getBoundingClientRect().left;
      cards.forEach(function (card, index) {
        var distance = Math.abs(card.getBoundingClientRect().left - trackLeft);
        if (distance < best) { best = distance; active = index; }
      });
      dots.forEach(function (dot, index) {
        dot.setAttribute('aria-current', String(index === active));
      });
    };
    track.addEventListener('scroll', function () { window.requestAnimationFrame(update); }, { passive: true });
    update();
  }
})();
