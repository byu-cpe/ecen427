---
layout: page
toc: false
title: Lab Help Calendar
indent: 0
number: 5
icon: fa fa-calendar
sidebar: true
---

Lab help hours are listed below. The calendar is published from Outlook, so it
always reflects the current schedule.

<div class="cal-embed">
  <iframe
    src="https://outlook.office365.com/owa/calendar/a03ee86c660149f3bdb2d115865b538d@byu.edu/8a019b4419684ccbbb2a3033caf70f6615832378305417721267/calendar.html"
    title="Lab Help Calendar"
    loading="lazy"></iframe>
</div>

<p class="cal-embed-link">
  Trouble viewing it?
  <a href="https://outlook.office365.com/owa/calendar/a03ee86c660149f3bdb2d115865b538d@byu.edu/8a019b4419684ccbbb2a3033caf70f6615832378305417721267/calendar.html"
     target="_blank" rel="noopener">Open the calendar in a new tab.</a>
</p>

<style>
/* The published Outlook calendar needs room: at a narrow width it clips the
   Saturday column and grows its own scrollbars. Let it fill the content column
   and scale its height with the viewport instead of a fixed 800x600 box. */
.cal-embed {
    width: 100%;
    height: 75vh;
    min-height: 600px;
    margin: 1rem 0 0.5rem;
}

.cal-embed iframe {
    width: 100%;
    height: 100%;
    border: 1px solid var(--cal-border, #dee2e6);
    border-radius: 4px;
}

.cal-embed-link {
    font-size: 0.85rem;
}

/* On a phone the month grid is unusable shrunk down, so give it a taller box
   and let the reader scroll it. */
@media (max-width: 820px) {
    .cal-embed {
        height: 70vh;
        min-height: 450px;
    }
}
</style>
