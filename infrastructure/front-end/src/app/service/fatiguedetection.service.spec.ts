import { TestBed } from '@angular/core/testing';

import { FatigueDetectionService } from './fatiguedetection.service';

describe('FatigueDetectionService', () => {
  let service: FatigueDetectionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FatigueDetectionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
