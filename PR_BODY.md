## Summary
This PR modernizes the Flask RESTful application by updating all packages to their latest versions and adding a comprehensive test suite with 96% code coverage.

### Package Updates
- **Flask**: 2.3.2 → 3.1.2 (major version upgrade)
- **Flask-RESTful**: 0.3.9 → 0.3.10
- **Flask-SQLAlchemy**: 2.5.1 → 3.1.1 (major version upgrade)
- **SQLAlchemy**: 1.4.19 → 2.0.44 (major version upgrade)
- **Flask-JWT-Extended**: 4.2.1 → 4.7.1
- **Werkzeug**: 3.0.1 → 3.1.3
- **Jinja2**: 3.1.3 → 3.1.6
- **python-dateutil**: 2.8.1 → 2.9.0.post0
- **pytz**: 2021.1 → 2025.2
- **psycopg2-binary**: (no version) → 2.9.10
- **rich**: (no version) → 13.9.4

### Flask 3.x Compatibility Fixes
- Replaced deprecated `@app.before_first_request` decorator (removed in Flask 3.0)
- Moved database initialization to module level
- Moved `db.create_all()` to `if __name__ == '__main__'` block
- Added JWT `user_lookup_loader` callback for proper authentication

### Test Suite (62 tests, 96% coverage)
Added comprehensive tests for:
- **Models** (21 tests): UserModel, ItemModel, StoreModel
- **Resources** (37 tests): All API endpoints with authentication tests
- **Utilities** (4 tests): JSON encoder and logger

#### Bug Fixes Discovered by Tests
1. Fixed Item.get() crash when item not found (app/resources/item.py:23)
2. Fixed Item.put() missing store_id when creating new items (app/resources/item.py:60)
3. Removed non-existent full_name field from User.get() response (app/resources/user.py:43)
4. Fixed SQLAlchemy relationship warnings with back_populates

### Configuration Improvements
- Added environment variable support for DATABASE_URL
- Test fixtures use SQLite in-memory database for fast, isolated tests
- Added pytest, pytest-flask, and pytest-cov dependencies

## Test Results
```
============================== 62 passed in 0.87s ==============================

---------- coverage: platform linux, python 3.11.14-final-0 ----------
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
app/__init__.py                 0      0   100%
app/app.py                     35      5    86%
app/config.py                   5      0   100%
app/db.py                       2      0   100%
app/models/item.py             23      0   100%
app/models/store.py            19      0   100%
app/models/user.py             21      0   100%
app/resources/item.py          48      2    96%
app/resources/store.py         31      2    94%
app/resources/user.py          39      0   100%
app/util/encoder.py            15      1    93%
app/util/logz.py               11      0   100%
---------------------------------------------------------
TOTAL                         249     10    96%
```

## Breaking Changes
None - all changes are backward compatible.

## Test Plan
- [x] All 62 tests pass
- [x] 96% code coverage achieved
- [x] Application imports successfully
- [x] All Python files have valid syntax
- [x] Package versions verified
