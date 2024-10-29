-- Users
INSERT INTO users (id, username, email, password, image) VALUES
(uuid_generate_v4(), 'alice_dev', 'alice@example.com', 'password123', NULL),
(uuid_generate_v4(), 'bob_dev', 'bob@example.com', 'password123', NULL),
(uuid_generate_v4(), 'carol_design', 'carol@example.com', 'password123', NULL);

-- Projects for Alice
INSERT INTO projects (id, user_id, name, icon, color) VALUES
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'alice_dev'), 'API Development', 'api_icon', '#ff5733'),
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'alice_dev'), 'Backend Refactoring', 'backend_icon', '#33c3ff');

-- Projects for Bob
INSERT INTO projects (id, user_id, name, icon, color) VALUES
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'bob_dev'), 'Frontend Revamp', 'frontend_icon', '#ffbd33'),
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'bob_dev'), 'User Dashboard', 'dashboard_icon', '#85ff33');

-- Projects for Carol
INSERT INTO projects (id, user_id, name, icon, color) VALUES
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'carol_design'), 'Brand Identity Redesign', 'brand_icon', '#ff33a6'),
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'carol_design'), 'Social Media Assets', 'media_icon', '#ff3333'),
(uuid_generate_v4(), (SELECT id FROM users WHERE username = 'carol_design'), 'Website Redesign', 'web_icon', '#33a6ff');

-- Tasks for Alice's Project: API Development
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'API Development'), (SELECT id FROM users WHERE username = 'alice_dev'), 'Define API structure', 'Define the structure and main endpoints for the API.', '#33ff57', FALSE, NOW(), NOW() + INTERVAL '14 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'API Development'), (SELECT id FROM users WHERE username = 'alice_dev'), 'Create endpoints for user management', 'Develop endpoints for user authentication and management.', '#33ff57', FALSE, NOW(), NOW() + INTERVAL '14 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'API Development'), (SELECT id FROM users WHERE username = 'alice_dev'), 'Write tests', 'Create unit and integration tests for the API.', '#33ff57', FALSE, NOW(), NOW() + INTERVAL '21 days');

-- Tasks for Alice's Project: Backend Refactoring
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Backend Refactoring'), (SELECT id FROM users WHERE username = 'alice_dev'), 'Analyze existing codebase', 'Conduct an analysis of the current codebase and database schema.', '#ff5733', FALSE, NOW(), NOW() + INTERVAL '7 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Backend Refactoring'), (SELECT id FROM users WHERE username = 'alice_dev'), 'Optimize queries', 'Optimize SQL queries to improve performance.', '#ff5733', FALSE, NOW(), NOW() + INTERVAL '14 days');

-- Tasks for Bob's Project: Frontend Revamp
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Frontend Revamp'), (SELECT id FROM users WHERE username = 'bob_dev'), 'Redesign homepage layout', 'Implement a new layout for the homepage.', '#ffbd33', FALSE, NOW(), NOW() + INTERVAL '10 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Frontend Revamp'), (SELECT id FROM users WHERE username = 'bob_dev'), 'Implement mobile responsiveness', 'Ensure the site is responsive on all device sizes.', '#ffbd33', FALSE, NOW(), NOW() + INTERVAL '15 days');

-- Tasks for Bob's Project: User Dashboard
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'User Dashboard'), (SELECT id FROM users WHERE username = 'bob_dev'), 'Build user profile page', 'Create a profile page where users can edit their information.', '#85ff33', FALSE, NOW(), NOW() + INTERVAL '7 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'User Dashboard'), (SELECT id FROM users WHERE username = 'bob_dev'), 'Add analytics widgets', 'Implement widgets that show analytics data on the dashboard.', '#85ff33', FALSE, NOW(), NOW() + INTERVAL '12 days');

-- Tasks for Carol's Project: Brand Identity Redesign
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Brand Identity Redesign'), (SELECT id FROM users WHERE username = 'carol_design'), 'Design new logo', 'Create a new logo that aligns with the rebranding.', '#ff33a6', FALSE, NOW(), NOW() + INTERVAL '20 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Brand Identity Redesign'), (SELECT id FROM users WHERE username = 'carol_design'), 'Define brand color scheme', 'Establish a new color scheme for the brand.', '#ff33a6', FALSE, NOW(), NOW() + INTERVAL '15 days');

-- Tasks for Carol's Project: Social Media Assets
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Social Media Assets'), (SELECT id FROM users WHERE username = 'carol_design'), 'Design Instagram template', 'Create a template for Instagram posts.', '#ff3333', FALSE, NOW(), NOW() + INTERVAL '5 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Social Media Assets'), (SELECT id FROM users WHERE username = 'carol_design'), 'Create Twitter header', 'Design a Twitter header image.', '#ff3333', FALSE, NOW(), NOW() + INTERVAL '8 days');

-- Tasks for Carol's Project: Website Redesign
INSERT INTO tasks (id, project_id, user_id, title, description, steps, color, is_completed, created_at, deadline) VALUES
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Website Redesign'), (SELECT id FROM users WHERE username = 'carol_design'), 'Create wireframes', 'Develop wireframes for the new website design.', '#33a6ff', FALSE, NOW(), NOW() + INTERVAL '14 days'),
(uuid_generate_v4(), (SELECT id FROM projects WHERE name = 'Website Redesign'), (SELECT id FROM users WHERE username = 'carol_design'), 'Design homepage layout', 'Create the visual layout for the homepage.', '#33a6ff', FALSE, NOW(), NOW() + INTERVAL '18 days');
