INSERT INTO categories (name, description, created_at) VALUES
('Version Updates', 'News and announcements about new releases and features in AbbyBot.', CURRENT_TIMESTAMP),
('Development Insights', 'Articles sharing insights and decisions made during the development of AbbyBot.', CURRENT_TIMESTAMP),
('Technical Roadmap', 'Plans and new features in development for AbbyBot.', CURRENT_TIMESTAMP),
('Security & Bug Fixes', 'Updates on security improvements and critical bug fixes in AbbyBot.', CURRENT_TIMESTAMP),
('Community Contributions', 'Acknowledging contributions from the community and new team members.', CURRENT_TIMESTAMP),
('Features in Focus', 'Detailed explanations and guides on key features of AbbyBot.', CURRENT_TIMESTAMP);


-- Create news
INSERT INTO news (title, content, image_url, category_id, created_at) VALUES
('AbbyBot Website v2.0.0 Released', 
 '<h2>We are pleased to announce the release of AbbyBot Website version 2.0.0!</h2> <p>In this version, we''ve improved the graphical interface compared to the first version, aiming for a cleaner, more attractive, and minimalist aesthetic. We have added new features and removed some unnecessary ones.</p>

<h3>Here’s the full changelog:</h3>

<ul>
  <li><strong>New index.html:</strong> We completely revamped the main page’s aesthetics, replacing the strong orange color, which was somewhat unpleasant for some users, with a more eye-friendly gradient.</li>
  <li><strong>Animations:</strong> Each section of the pages now features animations to better engage the viewer.</li>
  <li><strong>Removed ''Overview'' page:</strong> We replaced the Overview page by incorporating AbbyBot’s features directly into the main page. By scrolling down, all details can be seen.</li>
  <li><strong>News system:</strong> Updates and news will now be published through the /abbybot-news page, for a more convenient reading experience!</li>
  <li><strong>Improved Wishlist:</strong> We have refined the entire wishlist system to provide greater fluidity and robustness, enhancing both its appearance and functionality.</li>
  <li><strong>Statistics:</strong> AbbyBot pages now feature statistics that inform the user about the system, so they can stay updated with the latest information at any time.</li>
  <li><strong>Real-time Bot status:</strong> AbbyBot now has a renewed system to check its status, providing real-time updates on whether the Bot is online or offline.</li>
</ul>',
 'https://example.com/img/v1_release.jpg', 
 1, 
 CURRENT_TIMESTAMP);
